import React from "react";
import { NextPage } from "next";
import Layout from "../components/Layout/Signin";
import SignInForm from "../components/Form/SignIn";

const signin: NextPage = () => {
    return (
        <Layout>
            <SignInForm />
        </Layout>
    );
};

export default signin;
