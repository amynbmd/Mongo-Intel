
// jest.config.js
// module.exports = {
//   setupFilesAfterEnv: ["@testing-library/jest-dom/extend-expect"],
// };
// jest.config.js
// jest.config.js
module.exports = {
  setupFilesAfterEnv: ["@testing-library/jest-dom/extend-expect"],
  moduleNameMapper: {
    "^axios$": require.resolve("axios"),
    transformIgnorePatterns: ["/node_modules/(?!(axios)/)"],
  },
};

// // jest.config.js file

// const nextJest = require("next/jest");

// const createJestConfig = nextJest({ dir: "./" });

// const customJestConfig = {
//   // Custom Config Values
// };

// module.exports = async () => {
//   const asyncConfig = createJestConfig(customJestConfig);
//   const config = await asyncConfig();
//   const transformIgnorePatterns = ["node_modules/(?!axios)/"];
//   return { ...config, transformIgnorePatterns };
// };

module.exports = {
  transformIgnorePatterns: ["node_modules/(?!(axios)/)"],
};

