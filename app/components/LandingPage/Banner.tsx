import {
  chakra,
  Container,
  Stack,
  Text,
  Flex,
  SimpleGrid,
} from "@chakra-ui/react";
import Scale from "../Icon/Scale";
import File from "../Icon/File";
import Circle from "../Icon/Circle";
import { Fragment } from "react";

const features = [
  {
    title: "Free and open source",
    detail: "All components have MIT license, you can use in any project.",
    icon: <Scale />,
  },
  {
    title: "TypeScript based",
    detail: "Build type safe applications, all components and hooks export types.",
    icon: <File />,
  },
  {
    title: "Easy to customize",
    detail: "Build type safe applications, all components and hooks export types.",
    icon: <Circle />,
  },
];

const HeroSection = () => {
  return (
    <Fragment>
      <Container maxW="6xl" px={{ base: 6, md: 10 }} py={14}>
        <Stack
          direction={{ base: "column", md: "row" }}
          justifyContent="center"
        >
          <Stack direction="column" spacing={10} justifyContent="center">
            <chakra.h1
              fontSize="5xl"
              lineHeight={1}
              fontWeight="bold"
              textAlign="center"
            >
              No Hassle. {""}
              <chakra.span bg="#c900ff" bgClip="text">
                Just Train.
              </chakra.span>
            </chakra.h1>
            <Text
              color="gray.300"
              fontSize="xl"
              textAlign="center"
              fontWeight="400"
            >
              Build and customize your product with no limits or license fees.
              It is an open-source framework for scheduling deep learning
              training jobs.
            </Text>
            <SimpleGrid
              columns={{ base: 1, md: 3 }}
              placeItems="center"
              spacing={21}
            >
              {features.map((feature, index) => (
                <Stack p={10} borderRadius="xl" key={index} width="100%">
                  <Flex
                    p={3}
                    maxH="52px"
                    w="max-content"
                    color="white"
                    bg="#c900ff"
                    rounded="md"
                  >
                    {feature.icon}
                  </Flex>
                  <Stack direction="column" spacing={2}>
                    <Text fontSize="xl" fontWeight="500">
                      {feature.title}
                    </Text>
                    <Text
                      fontSize="md"
                      color="gray.400"
                      maxW={{ base: "100%", md: "200px" }}
                    >
                      {feature.detail}
                    </Text>
                  </Stack>
                </Stack>
              ))}
            </SimpleGrid>
          </Stack>
        </Stack>
      </Container>
    </Fragment>
  );
};

export default HeroSection;
