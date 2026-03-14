const FEISHU_APP_ID = 'cli_a93a5d6ab53b9bb4';
const FEISHU_APP_SECRET = 'X2Fl7ofdld5gwoxcNmnftg2wJ5kWFzZ1';
const BITABLE_APP_TOKEN = 'Y2UubXzPaaxk91sfxrRc9ffsnhc';
const BITABLE_TABLE_ID = 'tbla8AX3EfZGLbBt';

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

async function getAccessToken() {
  const res = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: FEISHU_APP_ID, app_secret: FEISHU_APP_SECRET }),
  });
  const data = await res.json();
  return data.tenant_access_token;
}

async function handleRequest(request) {
  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: CORS_HEADERS });
  }
  if (request.method !== 'POST') {
    return new Response('Method not allowed', { status: 405, headers: CORS_HEADERS });
  }
  try {
    const body = await request.json();
    const token = await getAccessToken();
    const fields = {
      '联系人': body.username || '',
      '电话': body.phone || '',
      '意向园区': body.region || '未确定',
      '需求面积': body.area || '',
      '来源平台': body.platform || '其他',
      '备注': [body.desc, body.url ? '链接：' + body.url : '', body.note || ''].filter(Boolean).join('\n'),
      '跟进状态': '待跟进',
    };
    const res = await fetch('https://open.feishu.cn/open-apis/bitable/v1/apps/' + BITABLE_APP_TOKEN + '/tables/' + BITABLE_TABLE_ID + '/records', {
      method: 'POST',
      headers: { 'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json' },
      body: JSON.stringify({ fields }),
    });
    const result = await res.json();
    return new Response(JSON.stringify({ ok: true, result }), {
      headers: { ...CORS_HEADERS, 'Content-Type': 'application/json' },
    });
  } catch (e) {
    return new Response(JSON.stringify({ ok: false, error: e.message }), {
      status: 500,
      headers: { ...CORS_HEADERS, 'Content-Type': 'application/json' },
    });
  }
}

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});
