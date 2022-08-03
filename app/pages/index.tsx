import type { NextPage } from 'next'
import '../styles/Home.module.css'
import { Heading } from '@chakra-ui/react'
import Layout from '../components/Layout'
import JobForm from '../components/Form/Job'

const Home: NextPage = () => {
  return (
    <Layout>
      <Heading as="h1">
        Schedulearn
      </Heading>
      <JobForm />
    </Layout>
  )
}

export default Home
