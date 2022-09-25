import "../styles/Home.module.css";
import { NextPage } from "next";
import Layout from "../components/Layout/Main";
import Heading from "../components/LandingPage/Heading";
import Banner from "../components/LandingPage/Banner";
import Howitworks from "../components/LandingPage/Howitworks";
import Footer from "../components/LandingPage/Footer";

const Home: NextPage = () => {
  return (
    <Layout>
      <Heading />
      <Banner />
      <Howitworks />
      <Footer />
    </Layout>
  );
};

export default Home;