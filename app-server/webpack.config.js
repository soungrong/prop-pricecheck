const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    entry: './app_server/src/index.js',
    output: {
        path: path.resolve(__dirname, 'app_server/static/js'),
        filename: 'bundle.js'
    },
    module: {
        rules: [{
            test: /\.(sa|sc|c)ss$/,
            use: [{
                    loader: MiniCssExtractPlugin.loader,
                    options: {
                        hmr: true,
                    },
                },
                'css-loader',
                'sass-loader',
            ],
        }]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: 'css/bulma.bundle.css'
        }),
    ]
};
