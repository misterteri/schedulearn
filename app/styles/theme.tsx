import {
  extendTheme,
  type ThemeConfig,
  theme as base,
  textDecoration,
} from "@chakra-ui/react";

const config: ThemeConfig = {
  initialColorMode: "dark",
  useSystemColorMode: false,
};

// customize fonts add "config" to the theme as well
const theme = extendTheme(
  { config },
  {
    ...extendTheme,
  }
);

export default theme;
