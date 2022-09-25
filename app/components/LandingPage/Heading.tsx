import * as React from "react";
import {
  Stack,
  chakra,
  Text,
  Button,
  Link,
  Heading,
  Box,
} from "@chakra-ui/react";

import { FaGithub } from "react-icons/fa";
const HeroSection = () => {
  return (
    <Stack direction="column" my="15rem" spacing={6} alignItems="center">
      <Heading
        fontSize={{ base: "3xl", sm: "4xl", md: "6xl" }}
        fontWeight="bold"
        textAlign="center"
        maxW="800px"
      >
        <chakra.span bg="#c900ff" bgClip="text">
          Training Models{" "}
        </chakra.span>
        Made Easy
      </Heading>
      <Text maxW="600px" fontSize="xl" textAlign="center" color="gray.400">
        Schedulearn is a simple yet poweful tool for scheduling deep learning
        training jobs.
      </Text>
      <Stack
        direction={{
          base: "column",
          sm: "row",
        }}
        spacing={2}
      >
        <Box display="inline-flex" rounded="md" shadow="md">
          <Button
            display="inline-flex"
            alignItems="center"
            justifyContent="center"
            px={5}
            py={3}
            border="solid transparent"
            fontWeight="bold"
            w="full"
            rounded="md"
            bg="#5d0076"
            _hover={{
              bg: "#8900ae",
              textDecoration: "none",
            }}
            size="lg"
          >
            <Link
              href="https://schedulearn-docs.vercel.app"
              isExternal
              _hover={{ textDecoration: "none" }}
            >
              Get Started
            </Link>
          </Button>
        </Box>
        <Box ml={3} display="inline-flex" rounded="md" shadow="md">
          <Button
            w="full"
            display="inline-flex"
            alignItems="center"
            justifyContent="center"
            px={5}
            py={3}
            border="solid transparent"
            fontWeight="bold"
            rounded="md"
            color="gray.800"
            bg="white"
            _hover={{
              bg: "brand.50",
            }}
            leftIcon={<FaGithub />}
            size="lg"
          >
            <Link
              href="https://github.com/bsraya/schedulearn"
              isExternal
              _hover={{ textDecoration: "none" }}
            >
              Github
            </Link>
          </Button>
        </Box>
      </Stack>
    </Stack>
  );
};

export default HeroSection;
