const CONTROLLER_URL = 'http://dev-logistics-wizard.mybluemix.net/api/v1';
// const ERP_URL = 'http://dev-logistics-wizard-erp.mybluemix.net/api/v1';

export const callApi = (endpoint, options = {}) =>
  fetch(`${options.apiUrl || CONTROLLER_URL}/${endpoint}`, {
    headers: options.headers || { 'Content-Type': 'application/json' },
    method: options.method || 'GET',
    body: options.body ? JSON.stringify(options.body) : undefined,
  })
  .then(response => response.json().then(json => ({ json, response })))
  .then(({ json, response }) => {
    if (!response.ok) throw json;

    return json;
  });

export const createDemo = (name, email) =>
  callApi('demos', {
    method: 'POST',
    body: { name, email },
  });

export const getDemo = (guid) => callApi(`demos/${guid}`);

export const login = (id, guid) =>
  callApi(`demos/${guid}/login`, {
    method: 'POST',
    body: { userId: id },
  });

export const getAdminData = token =>
  callApi('admin', { headers: { Authorization: `Bearer ${token}` } });

export const api = {
  createDemo,
  getDemo,
  login,
  getAdminData,
};

export default api;
