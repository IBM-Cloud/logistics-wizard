const CONTROLLER_URL = 'http://dev-logistics-wizard.mybluemix.net/api/v1';
const ERP_URL = 'http://dev-logistics-wizard-erp.mybluemix.net/api/v1';

export const controllerApi = (endpoint, method = 'GET', body) =>
  fetch(`${CONTROLLER_URL}/${endpoint}`, {
    headers: { 'Content-Type': 'application/json' },
    method,
    body: JSON.stringify(body),
  })
  .then(response => response.json().then(json => ({ json, response })))
  .then(({ json, response }) => {
    if (!response.ok) throw json;

    return json;
  });

export const createDemo = body => controllerApi('demos', 'POST', body);

export const api = {
  createDemo,
};

export default api;
