const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = {
    entry: {
        index: './app_server/src/index.js',
        form: './app_server/src/form.js',
        fontawesome: './node_modules/@fortawesome/fontawesome-free/js/all.min.js'
    },
    output: {
        path: path.resolve(__dirname, 'app_server/static'),
        filename: '[name].bundle.js'
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
            filename: 'app.bundle.css'
        }),
    ]
};
