module.exports = {
  jest: function (config) {
    config.transformIgnorePatterns = ["node_modules/(?!(axios)/)"];
    return config;
  },
};
