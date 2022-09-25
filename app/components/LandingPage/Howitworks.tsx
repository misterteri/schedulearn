import {
  Container,
  Box,
  chakra,
  Text,
  SimpleGrid,
  Heading,
} from "@chakra-ui/react";
interface IFeature {
  heading: string;
  content: string;
  step: number;
}

const features: IFeature[] = [
  {
    heading: "Learn with flashcards",
    content:
      "The main part of the learning process is using flashcards, you see a question, then you answer it.",
    step: 1,
  },
  {
    heading: "Never forget",
    content: `With our latest SRS algorithm, you will never forget what you've learned. The more you remember something, the less often the system will ask you to review it.`,
    step: 2,
  },
  {
    heading: "Tiny bits of information",
    content:
      "Instead of showing you a wall of text that will take you a long time to read and then that you quickly forget, we show you tiny bits of information every day.",
    step: 3,
  },
  {
    heading: "Community",
    content: `Keep your learning streak going, see stats of what you've learned and share it with others via your public profile. You can also join our private discord server!`,
    step: 4,
  },
];

const Features = () => {
  return (
    <Container maxW="6xl" p={{ base: 5, md: 10 }} my="10rem">
      <Heading fontSize="5xl" fontWeight="bold" mb={3} textAlign="center">
        How to Use {""}
        <chakra.span bg="#c900ff" bgClip="text">
          Schedulearn
        </chakra.span>{" "}
      </Heading>
      <SimpleGrid
        columns={{ base: 1, md: 2 }}
        placeItems="center"
        spacing={10}
        mt={12}
      >
        {features.map((feature, index) => (
          <Box
            key={index}
            boxShadow="xl"
            px={10}
            py={5}
            _hover={{
              boxShadow: "2xl",
              transform: "translateY(-2px)",
              transition: "all 0.2s",
            }}
            height="250px"
            bgColor="gray.800"
            borderRadius="xl"
          >
            <chakra.span
              bg=" #c900ff"
              bgClip="text"
              fontSize={{ base: "2xl", sm: "4xl" }}
              fontWeight="bold"
            >
              {feature.step}
            </chakra.span>
            <Heading as="h3" fontWeight="semibold" fontSize="2xl">
              {feature.heading}
            </Heading>
            <Text fontSize="md" mt={2}>
              {feature.content}
            </Text>
          </Box>
        ))}
      </SimpleGrid>
    </Container>
  );
};

export default Features;
