import { NextPage } from "next";
import Layout from "../components/Layout";
import LoginForm from "../components/Form/Login";

const login: NextPage = () => {
    return (
        <Layout>
            <LoginForm />
        </Layout>
    );
};

export default login;
