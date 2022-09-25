import type { NextPage } from "next";

import Form from "../components/Form/Job";
import Layout from "../components/Layout/Dashboard";

const Dashboard: NextPage = () => {
    return (
        <Layout>
            <Form />
        </Layout>
    );
};

export default Dashboard;