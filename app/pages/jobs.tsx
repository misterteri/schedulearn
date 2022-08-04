import type { NextPage } from "next";
import "../styles/Home.module.css";
import { Heading } from "@chakra-ui/react";
import Layout from "../components/Layout";
import JobTable from "../components/Table/Job";

type Job = {
    id: number;
    name: string;
    type: string;
    container_image: string;
    command: string;
    no_of_gpus: number;
};

const Jobs: NextPage = ({ jobs }: any) => {
    return (
        <Layout>
            <Heading as="h1">Jobs</Heading>
            <JobTable jobs={jobs} />
        </Layout>
    );
};

export async function getStaticProps() {
    const res = await fetch("http://localhost:5000/jobs");
    const jobs = await res.json();

    return {
        props: {
            jobs
        },
    };
}

export default Jobs;