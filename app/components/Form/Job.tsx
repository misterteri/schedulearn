import { Button } from "@chakra-ui/button";
import {
  VStack,
  Box,
  RadioGroup,
  Radio,
  FormControl,
  FormErrorMessage,
  FormLabel,
  Input,
  Container,
  Stack,
  Text,
  useToast
} from "@chakra-ui/react";
import { Field, Formik } from "formik";
import { useRouter } from "next/router";
import * as Yup from "yup";


function App() {
  const toast = useToast();
  const router = useRouter();

  return (
    <Container maxW="7xl" p={{ base: 15, md: 10 }}>
      <Box rounded="xl" height="100%" p={10} bgColor="#1B1B1B" boxShadow="lg">
        <Formik
          initialValues={{
            name: "",
            type: "",
            container_image: "",
            command: "",
            required_gpus: "",
          }}
          validationSchema={Yup.object({
            name: Yup.string()
              .required("Job name required")
              .min(10, "Job name should be at least 3 words"),

            type: Yup.string().required("Job type is required"),

            container_image: Yup.string()
              .required("Job image required")
              .min(10, "Job image should be at least 3 words"),

            command: Yup.string()
              .required("Job command required")
              .min(10, "Job command should be at least 3 words"),

            required_gpus: Yup.string().required("Number of GPU is required"),
          })}
          onSubmit={async (values) => {
            const res = await fetch("http://localhost:5000/jobs", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
              },
              body: JSON.stringify({
                name: values.name,
                type: values.type,
                container_image: values.container_image,
                command: values.command,
                required_gpus: parseInt(values.required_gpus),
              })
            });

            if (res.status === 201) {
              toast({
                title: "Success",
                description: "Job has been created",
                status: "success",
                duration: 5000,
                isClosable: true,
              })
            }

            router.push("/jobs")
          }}
        >
          {(formik) => (
            <form onSubmit={formik.handleSubmit}>
              <VStack>
                <FormControl
                  isInvalid={!!formik.errors.name && !!formik.touched.name}
                >
                  <FormLabel>Job Name</FormLabel>
                  <Input
                    id="name"
                    type="text"
                    placeholder="e.g. Sun Flower training"
                    {...formik.getFieldProps("name")}
                    onChange={formik.handleChange}
                    mb={3}
                  />
                  <FormErrorMessage>{formik.errors.name}</FormErrorMessage>
                </FormControl>

                <FormControl
                  isInvalid={!!formik.errors.type && !!formik.touched.type}
                >
                  <FormLabel>Job Type</FormLabel>

                  <RadioGroup id="type" {...formik.getFieldProps("type")}>
                    <Stack spacing={2} direction="row" mb={3}>
                      <Field
                        as={Radio}
                        type="radio"
                        id="type"
                        value="Tensorflow"
                      />
                      <Text>Tensorflow </Text>
                      <Field as={Radio} type="radio" id="type" value="Keras" />
                      <Text>Keras</Text>
                      <Field as={Radio} type="radio" id="type" value="MXnet" />
                      <Text>MXnet</Text>
                      <Field
                        as={Radio}
                        type="radio"
                        id="type"
                        value="Pytorch"
                      />
                      <Text>Pytorch</Text>
                    </Stack>
                  </RadioGroup>
                  <FormErrorMessage>{formik.errors.type}</FormErrorMessage>
                </FormControl>

                <FormControl
                  isInvalid={
                    !!formik.errors.container_image &&
                    !!formik.touched.container_image
                  }
                >
                  <FormLabel>Job Image</FormLabel>
                  <Input
                    id="container_image"
                    type="text"
                    placeholder="e.g. https://hub.docker.com/r/sunflowerai/sunflower-tf-gpu"
                    {...formik.getFieldProps("container_image")}
                    onChange={formik.handleChange}
                    mb={3}
                  />
                  <FormErrorMessage>
                    {formik.errors.container_image}
                  </FormErrorMessage>
                </FormControl>

                <FormControl
                  isInvalid={
                    !!formik.errors.command && !!formik.touched.command
                  }
                >
                  <FormLabel>Job Command</FormLabel>
                  <Input
                    id="command"
                    type="text"
                    placeholder="e.g. python train.py"
                    {...formik.getFieldProps("command")}
                    onChange={formik.handleChange}
                    mb={3}
                  />
                  <FormErrorMessage>{formik.errors.command}</FormErrorMessage>
                </FormControl>

                <FormControl
                  isInvalid={
                    !!formik.errors.required_gpus &&
                    !!formik.touched.required_gpus
                  }
                >
                  <FormLabel>Number of GPU(s)</FormLabel>
                  <RadioGroup
                    id="required_gpus"
                    {...formik.getFieldProps("required_gpus")}
                  >
                    <Stack spacing={2} direction="row" mb={3}>
                      <Field
                        as={Radio}
                        type="radio"
                        id="required_gpus"
                        value="1"
                      />
                      <Text>1</Text>
                      <Field
                        as={Radio}
                        type="radio"
                        id="required_gpus"
                        value="2"
                      />
                      <Text>2</Text>
                      <Field
                        as={Radio}
                        type="radio"
                        id="required_gpus"
                        value="3"
                      />
                      <Text>3</Text>
                      <Field
                        as={Radio}
                        type="radio"
                        id="required_gpus"
                        value="4"
                      />
                      <Text>4</Text>
                    </Stack>
                  </RadioGroup>

                  <FormErrorMessage>
                    {formik.errors.required_gpus}
                  </FormErrorMessage>
                </FormControl>

                <Button
                  w={{ base: "100%", sm: "auto" }}
                  h={12}
                  px={6}
                  rounded="3xl"
                  mb={{ base: 2, sm: 0 }}
                  bgColor="transparent"
                  borderColor="gray.200"
                  border="2px solid"
                  type="submit"
                >
                  Submit
                </Button>
              </VStack>
            </form>
          )}
        </Formik>
      </Box>
    </Container>
  );
}

export default App;
