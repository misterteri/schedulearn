import React from "react";
import { NextPage } from "next";
import Layout from "../components/Layout/Signin";
import SignUpForm from "../components/Form/SignUp";

const signup: NextPage = () => {
    return (
        <Layout>
            <SignUpForm />
        </Layout>
    );
};

export default signup;