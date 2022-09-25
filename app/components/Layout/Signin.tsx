import { Box, Container } from "@chakra-ui/react";
import Navbar from "../Navbar/Signin";

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <Box
      as="main"
      bgGradient={`linear(#000000,#1B1B1B, #2A1E36, #3A2152, #49236D, #582688)`}
      minH="100vh"
    >
      <Navbar />
      <Container maxW="container.lg">{children}</Container>
    </Box>
  );
};

export default Layout;
