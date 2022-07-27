import { Box, Container } from '@chakra-ui/react'

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    return (
        <Box as="main">
            <Container
                my={10}
                maxW="container.md"
            >
                {children}
            </Container>
        </Box>
    );
}

export default Layout