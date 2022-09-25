import Layout from "../../components/Layout/Dashboard";
import { useEffect, useState } from "react";
import { Box, Code, Heading, useColorModeValue, VStack } from "@chakra-ui/react";

export default function JobOverview({ job }: { job: any }) {
  const [output, setOutput] = useState<string[]>([]);
  const hoverColor = useColorModeValue("gray.200", "gray.500")

  // fetch docker output with useEffect
  const fetchDockerOutput = useEffect(() => {
    const ws = new WebSocket(`ws://localhost:5000/jobs/${job.id}/logs`);
    ws.onmessage = (event: any) => {
      setOutput((test: string[]) => [...test, event.data]);
    }
  }, []);

  return (
    <Layout>
      <Box>
        <Heading as="h1" fontSize="2xl">{job.name}</Heading>
        <p>Type: {job.type}</p>
        <p>Number of required GPUs: {job.required_gpus}</p>
        <p>Container image: {job.container_image}</p>
        <p>Command: {job.command}</p>
      </Box>

      <Heading as="h2" mt={10} mb={5}>Training Status</Heading>
      <details
        onClick={() => fetchDockerOutput}
        style={{
          border: "1px solid #ccc",
          borderRadius: "0.5rem",
        }}
      >
        <summary style={{ padding: "1rem", marginLeft: "0.5rem" }}>Output</summary>
        <VStack
          align="flex-start"
          spacing={1}
        >
          {output.map((line, index) => (
            <Code
              key={index}
              bg="none"
              _hover={{
                bg: hoverColor
              }}
              width="100%"
              fontSize="md"
              px={5}
            >{line}</Code>
          ))}
        </VStack>
      </details>
    </Layout>
  )
}

export const getStaticPaths = async () => {
  const res = await fetch("http://localhost:5000/jobs");
  const jobs = await res.json();
  const paths = jobs.map((job: any) => ({
    params: { id: String(job.id) },
  }));

  return { paths, fallback: false };
}

export const getStaticProps = async ({ params: { id } }: { params: { id: string } }) => {
  const res = await fetch(`http://localhost:5000/jobs/${id}`);
  const job = await res.json();

  return { props: { job } };
}