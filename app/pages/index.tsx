import type { NextPage } from 'next'
import '../styles/Home.module.css'
import Form from '../components/Form'
import { Heading } from '@chakra-ui/react'
import Layout from '../components/Layout'

const Home: NextPage = () => {
  return (
    <Layout>
      <Heading as="h1">
        Schedulearn
      </Heading>
      <Form />
    </Layout>
  )
}

export default Home
