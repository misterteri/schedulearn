import {
  Td,
  Th,
  Tr,
  Flex,
  Thead,
  Tbody,
  Table,
  Spinner,
  TableContainer,
  useColorMode,
  Link
} from "@chakra-ui/react";
import DeleteJob from "../Button/DeleteJob";
import NextLink from "next/link";

type Job = {
  id: number;
  name: string;
  type: string;
  container_image: string;
  command: string;
  required_gpus: number;
  created_at: string;
  started_at: string;
  completed_at: string;
};

const JobTable = ({ jobs }: { jobs: Job[] }) => {
  // get the current color mode
  const { colorMode } = useColorMode();
  const depth = (colorMode === "dark") ? "500" : "200";
  return (
    // if jobs is empty, show "No jobs found"
    // if the jobs have not been loaded, show <Spinner />
    <>
      {jobs.length === 0 ? (
        <Flex justifyContent="center" alignItems="center">
          <Spinner
            thickness='4px'
            speed='0.65s'
            emptyColor='gray.200'
            color='blue.500'
            size='xl'
          />
        </Flex>
      ) : (
        <TableContainer>
          <Table>
            <Thead>
              <Tr>
                <Th></Th>
                <Th>Name</Th>
                <Th>Type</Th>
                <Th>GPU(s)</Th>
                <Th>Container Image</Th>
              </Tr>
            </Thead>
            <Tbody>
              {jobs.map((job: Job) => (
                <Tr
                  key={job.id}
                  // if job.created_at exists, but job.started_at does not, set the background color to red
                  // if job.created_at and job.completed_at exist, set the background color to blue.200
                  // if job.started_at and job.completed_at exist, set the background color to green.200
                  bg={
                    job.created_at && !job.started_at
                      ? `red.${depth}`
                      : job.created_at && job.started_at && !job.completed_at
                        ? `blue.${depth}`
                        : job.completed_at
                          ? `green.${depth}`
                          : "white"
                  }
                >
                  <Td><DeleteJob id={job.id} /></Td>
                  <Td>
                    <NextLink
                      href="/jobs/[id]"
                      as={`/jobs/${job.id}`}
                    >
                      <Link _hover={{
                        textDecoration: "underline",
                      }}>
                        {job.name}
                      </Link>
                    </NextLink>
                  </Td>
                  <Td>{job.type}</Td>
                  <Td>{job.required_gpus}</Td>
                  <Td>{job.container_image}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </TableContainer>
      )}
    </>
  );
};

export default JobTable;
