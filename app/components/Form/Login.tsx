import { Formik, Field } from "formik";
import {
    FormLabel,
    FormControl,
    Input,
    Stack,
    Button,
    Heading,
    Text,
    Box,
    FormErrorMessage,
    useColorModeValue,
    VStack
} from "@chakra-ui/react";

const LoginForm = () => {
    return (
        <Box>
            <Stack align="center" spacing={2} mb={5}>
                <Heading fontSize={{ base: "xl", sm: "3xl" }}>
                    Sign in to your account
                </Heading>
                <Text fontSize={{ base: "sm", sm: "md" }}>
                    Send a magic link to your email
                </Text>
            </Stack>
            <Box
                pos="relative"
                p={10}
                bg={useColorModeValue("white", "gray.700")}
                rounded="lg"
                boxShadow="lg"
            >
                <Formik
                    initialValues={{
                        email: ""
                    }}

                    onSubmit={(values) => {
                        alert(JSON.stringify(values, null, 2));
                    }}
                >
                    {({ handleSubmit, errors, touched }) => (
                        <form onSubmit={handleSubmit}>
                            <VStack spacing={4} align="flex-start">
                                <FormControl
                                    isInvalid={!!errors.email && !!touched.email}
                                >
                                    <FormLabel htmlFor="email">Email address <span style={{ color: "red" }}>*</span></FormLabel>
                                    <Field
                                        as={Input}
                                        id="email"
                                        name="email"
                                        type="email"
                                        variant="filled"
                                        validate={(value: string) => {
                                            let error;

                                            // value should have only "@gapp.nthu.edu.tw" or "@office365.nthu.edu.tw"
                                            if (!value.includes("@gapp.nthu.edu.tw") && !value.includes("@office365.nthu.edu.tw")) {
                                                error = "Email is not valid";
                                            }

                                            return error;
                                        }}
                                    />
                                    <FormErrorMessage>{errors.email}</FormErrorMessage>
                                </FormControl>
                                <Button
                                    bg="blue.400"
                                    color="white"
                                    _hover={{
                                        bg: "blue.500",
                                    }}
                                    rounded="md"
                                    w="100%"
                                    type="submit"
                                >
                                    Send magic link
                                </Button>
                            </VStack>
                        </form>
                    )}
                </Formik>
            </Box>
        </Box>
    );
};

export default LoginForm;
