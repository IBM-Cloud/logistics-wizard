import WebpackHotMiddleware from 'webpack-hot-middleware';
import _debug from 'debug';
import applyExpressMiddleware from '../libs/apply-express-middleware';

const debug = _debug('app:server:webpack-hmr');

export default function (compiler, opts) {
  debug('Enable Webpack Hot Module Replacement (HMR).');

  const middleware = WebpackHotMiddleware(compiler, opts);
  return async function koaWebpackHMR(ctx, next) {
    const hasNext = await applyExpressMiddleware(middleware, ctx.req, ctx.res);

    if (hasNext && next) {
      await next();
    }
  };
}
