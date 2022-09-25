import React from "react";
import { NextPage } from "next";
import Layout from "../components/Layout/Dashboard";
import ViewProfile from "../components/Logout/View_profile";

const signup: NextPage = () => {
    return (
        <Layout>
            <ViewProfile />
        </Layout>
    );
};

export default signup;