const path = require('path');
const webpack = require("webpack");
const BundleTracker = require('webpack-bundle-tracker');

module.exports = {
  context: __dirname,
  entry: {
    main: './frontend/fucker'
  },
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, './frontend/bundles')
  },
  module: {
    rules: [
    {
      test: /\.js$/,
      exclude: /(node_modules)/,
      use: {
        loader: 'babel-loader',
        options: {
          presets: ["react", "es2015", "stage-2"]
        }
      }
    }
    ]
  },
  resolve: {
    modules: ["node_modules"],
    extensions: ['.js']
  },
  plugins: [
    new BundleTracker({filename: "./webpack-dev-stats.json"}),
  ]
};

