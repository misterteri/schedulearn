import { Box, Container } from '@chakra-ui/react'
import Navbar from './Navbar'

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    return (
        <Box as="main">
            <Navbar />
            <Container
                my={10}
                maxW="container.lg"
            >
                {children}
            </Container>
        </Box>
    );
}

export default Layout