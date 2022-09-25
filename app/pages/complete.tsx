import { NextPage } from "next";
import { Box, Text, Container } from "@chakra-ui/react";
import Layout from "../components/Layout/Main";

const complete: NextPage = () => {
    return (
        <Layout>
            <Container my="8rem" maxW="xl" p={{ base: 5, md: 10 }}>

                <Box textAlign="center" p={10} bgColor="#1B1B1B" boxShadow="lg" rounded="xl">
                    <Text as="h1" fontSize="4xl" color="white">
                        <strong>Check Your Email</strong>
                    </Text>
                    <Text fontSize="m" color="white">
                        A sign in has been sent to your email
                    </Text>
                </Box>
            </Container>

        </Layout>
    );
};

export default complete;