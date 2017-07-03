const webpack = require('webpack');
const WebpackVisualizer = require('webpack-visualizer-plugin');

const API_URL = {
  production: JSON.stringify('yelp-beans.appspot.com'),
  development: JSON.stringify('localhost:8080'),
}
const environment = process.env.NODE_ENV === 'production' ? 'production' : 'development';

const VENDOR = [
  'axios',
  'moment-timezone',
  'react',
  'react-dom',
  'react-redux',
  'react-router',
  'redux',
  'redux-promise',
];

module.exports = {
  entry: {
    app: './index.jsx',
    vendor: VENDOR,
  },
  output: {
    publicPath: __dirname,
    path: __dirname,
    filename: 'dist/bundle/[name].bundle.js',
  },
  module: {
    rules: [
      {
        use: 'eslint-loader?{fix: true}',
        test: /\.jsx?$/,
        exclude: /node_modules/,
        enforce: 'pre',
      },
      {
        use: 'babel-loader',
        test: /\.jsx?$/,
        exclude: /node_modules/,
      },
    ],
  },
  devtool: 'source-map',
  devServer: {
    contentBase: './',
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  plugins: [
    new webpack.DefinePlugin({
      API_URL: API_URL[environment],
    }),
    new webpack.optimize.CommonsChunkPlugin({
      name: 'vendor',
      minChunks: Infinity,
    }),
    new WebpackVisualizer({
      filename: './dist/webpack.stats.html',
    }),
  ],
};
