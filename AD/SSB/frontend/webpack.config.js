module.exports = {
    entry: './src/main.js',
    module: {
        rules: [
            {
                test: /\.(png|svg|jpg|jpeg|gif|ico)$/,
                exclude: /node_modules/,
                use: ['file-loader?name=[name].[ext]']
            }
        ]
    }
}
