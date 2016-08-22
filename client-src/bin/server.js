import _debug from 'debug';
import opn from 'opn';
import config from '../config';
import server from '../server/main';

const debug = _debug('app:bin:server');
const port = config.server_port;
const host = config.server_host;

server.listen(port);
debug(`Server is now running at http://${host}:${port}.`);
debug(`Server accessible via localhost:${port}`);
opn(`http://localhost:${port}`);
