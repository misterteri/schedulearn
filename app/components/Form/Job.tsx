import {
    Box,
    useColorModeValue,
    VStack,
    FormControl,
    FormLabel,
    Button,
    Input,
    FormErrorMessage,
    Select,
    useToast
} from "@chakra-ui/react";
import { Formik, Field } from "formik";
import { useRouter } from 'next/router'

export default function JobForm(): JSX.Element {
    const toast = useToast();
    const router = useRouter();
    return (
        <Box
            pos="relative"
            p={10}
            bg={useColorModeValue("white", "gray.700")}
            rounded="lg"
            boxShadow="lg"
        >
            <Formik
                initialValues={{
                    name: "",
                    type: "",
                    container_image: "",
                    command: "",
                    required_gpus: 0,
                }}

                onSubmit={async (values) => {
                    const res = await fetch("http://localhost:5000/jobs", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify(values),
                    });
                    if (res.status === 201) {
                        toast({
                            title: "Success",
                            description: "Job has been created",
                            status: "success",
                            duration: 9000,
                            isClosable: true,
                        });
                    }
                    router.push("/jobs");
                }}
            >
                {({ handleSubmit, errors, touched }) => (
                    <form onSubmit={handleSubmit}>
                        <VStack spacing={4} align="flex-start">
                            <FormControl isInvalid={!!errors.name && !!touched.name}>
                                <FormLabel>Job Name</FormLabel>
                                <Field
                                    as={Input}
                                    id="name"
                                    name="name"
                                    type="text"
                                    variant="filled"
                                    placeholder="e.g. Sun Flower training"
                                    validate={(value: string) => {
                                        let error;
                                        if (value.length < 3) {
                                            error = "Job name should be at least 3 characters";
                                        }
                                        return error;
                                    }}
                                />
                                <FormErrorMessage>{errors.name}</FormErrorMessage>
                            </FormControl>

                            <FormControl isInvalid={!!errors.type && !!touched.type}>
                                <FormLabel>Job Type</FormLabel>
                                <Field
                                    as={Select}
                                    id="type"
                                    name="type"
                                    variant="filled"
                                    validate={(value: string) => {
                                        let error;
                                        //value must be chosen
                                        if (value === "") {
                                            error = "Job type is required";
                                        }
                                        return error;
                                    }}
                                >
                                    <option value="">Select job type</option>
                                    <option value="TensorFlow">TensorFlow</option>
                                    <option value="Pytorch">Pytorch</option>
                                    <option value="Keras">Keras</option>
                                </Field>
                                <FormErrorMessage>{errors.type}</FormErrorMessage>
                            </FormControl>

                            <FormControl isInvalid={!!errors.container_image && !!touched.container_image}>
                                <FormLabel>Job Image</FormLabel>
                                <Field
                                    as={Input}
                                    id="container_image"
                                    name="container_image"
                                    type="text"
                                    variant="filled"
                                    placeholder="e.g. https://hub.docker.com/r/sunflowerai/sunflower-tf-gpu"
                                    validate={(value: string) => {
                                        let error;
                                        //value cannot be empty
                                        if (value.length < 1) {
                                            error = "Job image is required";
                                        }
                                        return error;
                                    }}
                                />
                                <FormErrorMessage>{errors.container_image}</FormErrorMessage>
                            </FormControl>

                            <FormControl isInvalid={!!errors.command && !!touched.command}>
                                <FormLabel>Job Command</FormLabel>
                                <Field
                                    as={Input}
                                    id="command"
                                    name="command"
                                    type="text"
                                    variant="filled"
                                    placeholder="e.g. python train.py"
                                    validate={(value: string) => {
                                        let error;
                                        //value cannot be empty
                                        if (value.length < 1) {
                                            error = "Command is required";
                                        }
                                        return error;
                                    }}
                                />
                                <FormErrorMessage>{errors.command}</FormErrorMessage>
                            </FormControl>

                            <FormControl
                                isInvalid={!!errors.required_gpus && !!touched.required_gpus}
                            >
                                <FormLabel>Number of GPU</FormLabel>
                                <Field
                                    as={Select}
                                    id="required_gpus"
                                    name="required_gpus"
                                    type="number"
                                    variant="filled"
                                    validate={(value: number) => {
                                        let error;
                                        //input value need to be in range 1 until 4
                                        if (value < 1 || value > 4) {
                                            error = "Number of GPU is required";
                                        }
                                        return error;
                                    }}
                                >
                                    <option value="">Select number of GPU</option>
                                    <option value="1">1</option>
                                    <option value="2">2</option>
                                    <option value="3">3</option>
                                    <option value="4">4</option>
                                </Field>
                                <FormErrorMessage>{errors.required_gpus}</FormErrorMessage>
                            </FormControl>

                            <Button
                                bg="blue.400"
                                color="white"
                                _hover={{
                                    bg: "blue.500",
                                }}
                                rounded="md"
                                type="submit"
                            >
                                Submit
                            </Button>
                        </VStack>
                    </form>
                )}
            </Formik>
        </Box>
    );
}
