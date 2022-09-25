import { Formik, Field } from "formik";
import {
    FormLabel,
    FormControl,
    Input,
    Stack,
    Button,
    Heading,
    Box,
    Container,
    FormErrorMessage
} from "@chakra-ui/react";
import { useRouter } from "next/router";

export default function SignUpForm() {
    const router = useRouter();

    return (
        <Container my="4rem" maxW="xl" p={{ base: 5, md: 10 }}>
            <Stack align="center" spacing={4} mb={5}>
                <Heading fontSize={{ base: "xl", sm: "3xl" }}>
                    Sign up to Schedulearn
                </Heading>
            </Stack>
            <Box p={10} bgColor="#1B1B1B" boxShadow="lg" rounded="xl">
                <Formik
                    initialValues={{
                        email: "",
                        password: ""
                    }}
                    onSubmit={async (values) => {
                        const res = await fetch("http://localhost:5000/signup", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                                "Access-Control-Allow-Origin": "*",
                            },
                            body: JSON.stringify({
                                email: values.email,
                                password: values.password,
                            })
                        });
                        const data = await res.json();
                        if (res.status === 200) {
                            console.log(data);
                            router.push("/complete");
                        }
                    }}
                >
                    {({ handleSubmit, errors, touched }) => (
                        <form onSubmit={handleSubmit}>
                            <Stack spacing={4} alignContent="center">
                                <FormControl isInvalid={!!errors.email && !!touched.email}>
                                    <FormLabel htmlFor="email">
                                        Email address <span style={{ color: "red" }}>*</span>
                                    </FormLabel>
                                    <Field
                                        as={Input}
                                        id="email"
                                        name="email"
                                        type="email"
                                        variant="filled"
                                        validate={(value: string) => {
                                            let error;
                                            if (
                                                !value.includes("@gapp.nthu.edu.tw") &&
                                                !value.includes("@office365.nthu.edu.tw")
                                            ) {
                                                error = "Email is not valid";
                                            }

                                            return error;
                                        }}
                                    />
                                    <FormErrorMessage>{errors.email}</FormErrorMessage>
                                </FormControl>
                                <FormControl isInvalid={!!errors.password && !!touched.password}>
                                    <FormLabel htmlFor="password">
                                        Password <span style={{ color: "red" }}>*</span>
                                    </FormLabel>
                                    <Field
                                        as={Input}
                                        id="password"
                                        name="password"
                                        type="password"
                                        variant="filled"
                                        validate={(value: string) => {
                                            let error;
                                            if (value.length < 8) {
                                                error = "Password must be at least 8 characters";
                                            }
                                            return error;
                                        }}
                                    />
                                    <FormErrorMessage>{errors.password}</FormErrorMessage>
                                </FormControl>
                                <Button
                                    h={12}
                                    px={6}
                                    mb={{ base: 2, sm: 0 }}
                                    type="submit"
                                    bg="#5d0076"
                                    _hover={{
                                        bg: "#8900ae",
                                        textDecoration: "none",
                                    }}
                                >
                                    Sign up
                                </Button>
                            </Stack>
                        </form>
                    )}
                </Formik>
            </Box>
        </Container>
    )
}