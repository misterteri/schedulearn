import Layout from "../../components/Layout";
import { Box, Heading } from "@chakra-ui/react";

export default function JobOverview({ job }: { job: any }) {
  return (
    <Layout>
      <Box>
        <Heading as="h1" >{job.name}</Heading>
        <p>Type: {job.type}</p>
        <p>Number of required GPUs: {job.no_of_gpus}</p>
        <p>Container image: {job.container_image}</p>
        <p>Command: {job.command}</p>
      </Box>
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
  const res = await fetch(`http://localhost:5000/jobs`);
  const jobs = await res.json();

  // get the job object with the same id as the id in the params
  const job = jobs.find((job: any) => job.id === Number(id));

  return { props: { job } };
}