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
    GridItem,
    SimpleGrid,
    Select,
} from "@chakra-ui/react";
import NextLink from "next/link";
import { useRouter } from "next/router";
import { chakra } from "@chakra-ui/react";

export default function ViewProfile() {
    const router = useRouter();

    return (
        <Box mt={[10, 0]}>
            <SimpleGrid
                display={{
                    base: "initial",
                    md: "grid",
                }}
                columns={{
                    md: 3,
                }}
                spacing={{
                    md: 6,
                }}
            >
                <GridItem
                    colSpan={{
                        md: 1,
                    }}
                >
                    <Box px={[4, 0]}>
                        <Heading fontSize="lg" fontWeight="medium" lineHeight="6">
                            Personal Information
                        </Heading>
                        <Text
                            mt={1}
                            fontSize="sm"
                            color="gray.600"
                            _dark={{
                                color: "gray.400",
                            }}
                        >
                            Use a permanent address where you can receive mail.
                        </Text>
                    </Box>
                </GridItem >
                <GridItem
                    mt={[5, null, 0]}
                    colSpan={{
                        md: 2,
                    }}
                >
                    <chakra.form
                        method="POST"
                        shadow="base"
                        rounded={[null, "md"]}
                        overflow={{
                            sm: "hidden",
                        }}
                    >
                        <Stack
                            px={4}
                            py={5}
                            p={[null, 6]}
                            bg="white"
                            _dark={{
                                bg: "#141517",
                            }}
                            spacing={6}
                        >
                            <SimpleGrid columns={6} spacing={6}>

                                <FormControl as={GridItem} colSpan={[6, 4]}>
                                    <FormLabel
                                        htmlFor="name"
                                        fontSize="sm"
                                        fontWeight="md"
                                        color="gray.700"
                                        _dark={{
                                            color: "gray.50",
                                        }}
                                    >
                                        Full Name
                                    </FormLabel>
                                    <Input
                                        type="text"
                                        name="name"
                                        id="name"
                                        autoComplete="given-name"
                                        mt={1}
                                        focusBorderColor="brand.400"
                                        shadow="sm"
                                        size="sm"
                                        w="full"
                                        rounded="md"
                                    />
                                </FormControl>

                                <FormControl as={GridItem} colSpan={[6, 4]}>
                                    <FormLabel
                                        htmlFor="email"
                                        fontSize="sm"
                                        fontWeight="md"
                                        color="gray.700"
                                        _dark={{
                                            color: "gray.50",
                                        }}
                                    >
                                        Username
                                    </FormLabel>
                                    <Input
                                        type="text"
                                        name="email"
                                        id="email"
                                        autoComplete="email"
                                        mt={1}
                                        focusBorderColor="brand.400"
                                        shadow="sm"
                                        size="sm"
                                        w="full"
                                        rounded="md"
                                    />
                                </FormControl>

                                <FormControl as={GridItem} colSpan={[6, 3]}>
                                    <FormLabel
                                        htmlFor="degree"
                                        fontSize="sm"
                                        fontWeight="md"
                                        color="gray.700"
                                        _dark={{
                                            color: "gray.50",
                                        }}
                                    >
                                        Degree
                                    </FormLabel>
                                    <Select
                                        id="degree"
                                        name="degree"
                                        autoComplete="degree"
                                        placeholder="Select option"
                                        mt={1}
                                        focusBorderColor="brand.400"
                                        shadow="sm"
                                        size="sm"
                                        w="full"
                                        rounded="md"
                                    >
                                        <option>Bachelor</option>
                                        <option>Master</option>
                                        <option>Doctor</option>
                                        <option>Professor</option>
                                    </Select>
                                </FormControl>

                                <FormControl as={GridItem} colSpan={[6, 2]}>
                                    <FormLabel
                                        htmlFor="grade"
                                        fontSize="sm"
                                        fontWeight="md"
                                        color="gray.700"
                                        _dark={{
                                            color: "gray.50",
                                        }}
                                    >
                                        Grade
                                    </FormLabel>
                                    <Select
                                        id="grade"
                                        name="grade"
                                        autoComplete="grade"
                                        placeholder="Select option"
                                        mt={1}
                                        focusBorderColor="brand.400"
                                        shadow="sm"
                                        size="sm"
                                        w="full"
                                        rounded="md"
                                    >
                                        <option>1</option>
                                        <option>2</option>
                                        <option>3</option>
                                        <option>4</option>
                                        <option>4+</option>
                                    </Select>
                                </FormControl>

                                <FormControl as={GridItem} colSpan={6}>
                                    <FormLabel
                                        htmlFor="department"
                                        fontSize="sm"
                                        fontWeight="md"
                                        color="gray.700"
                                        _dark={{
                                            color: "gray.50",
                                        }}
                                    >
                                        Department
                                    </FormLabel>
                                    <Input
                                        type="text"
                                        name="department"
                                        id="department"
                                        autoComplete="department"
                                        mt={1}
                                        focusBorderColor="brand.400"
                                        shadow="sm"
                                        size="sm"
                                        w="full"
                                        rounded="md"
                                    />
                                </FormControl>
                            </SimpleGrid>
                            <Button
                                type="submit"
                                width="200px"
                                //TODO: send the button to the right 
                                ml="auto"
                                colorScheme="red"
                                _focus={{
                                    shadow: "",
                                }}
                                fontWeight="md"
                            >
                                Save
                            </Button>
                        </Stack>
                    </chakra.form>
                </GridItem>
            </SimpleGrid >
        </Box >
    )
}
