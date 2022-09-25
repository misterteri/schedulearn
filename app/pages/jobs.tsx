import type { NextPage } from "next";
import "../styles/Home.module.css";
import { Heading } from "@chakra-ui/react";
import Layout from "../components/Layout/Jobs";
import { useEffect, useState } from "react";
import JobTable from "../components/JobTable/JobTable";

const Jobs: NextPage = () => {
    const [jobs, setJobs] = useState([]);

    useEffect(() => {
        async function fetchJobs() {
            const res = await fetch("http://localhost:5000/jobs");
            const data = await res.json();
            console.log(data);
            setJobs(data);
        }
        fetchJobs();
    }, []);

    return (
        <Layout>
            <Heading as="h1">Jobs</Heading>
            <JobTable jobs={jobs} />
        </Layout>
    );
};

export default Jobs;
