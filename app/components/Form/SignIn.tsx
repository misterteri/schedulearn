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
  Text,
  FormErrorMessage,
  Link,
} from "@chakra-ui/react";
import NextLink from "next/link";
import { useRouter } from "next/router";

export default function SignInForm() {
  const router = useRouter();

  return (
    <Container my="4rem" maxW="xl" p={{ base: 5, md: 10 }}>
      <Stack align="center" spacing={4} mb={5}>
        <Heading fontSize={{ base: "xl", sm: "3xl" }}>
          Sign in to Schedulearn
        </Heading>
      </Stack>
      <Box p={10} bgColor="#1B1B1B" boxShadow="lg" rounded="xl">
        <Formik
          initialValues={{
            email: "",
            password: ""
          }}
          onSubmit={async (values) => {
            const res = await fetch("http://localhost:5000/signin", {
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
              // save the data to local storage
              localStorage.setItem("username", data.username);
              localStorage.setItem("email", data.email);
              localStorage.setItem("token", data.token);
              router.push("/dashboard");
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
                  w={{ base: "100%", sm: "auto" }}
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
                  Sign in
                </Button>
              </Stack>
            </form>
          )}
        </Formik>
      </Box>
      <Stack mt={5}>
        <Text mx="auto">Do not have an account? <NextLink href="/signup"><Link color="red.400" fontWeight="bold">Sign up here</Link></NextLink></Text>
      </Stack>
    </Container>
  );
};