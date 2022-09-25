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
} from "@chakra-ui/react";
import DeleteButton from "./DeleteButton";

type Job = {
  id: number;
  name: string;
  type: string;
  container_image: string;
  command: string;
  no_of_gpus: number;
};

const JobTable = ({ jobs }: { jobs: Job[] }) => {
  return (
    <>
      {jobs.length === 0 ? (
        <Flex justifyContent="center" alignItems="center">
          <Spinner
            thickness="4px"
            speed="0.65s"
            emptyColor="gray.200"
            color="blue.500"
            size="xl"
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
                <Th>Command</Th>
              </Tr>
            </Thead>
            <Tbody>
              {jobs.map((job) => (
                <Tr key={job.id}>
                  <Td>
                    <DeleteButton id={job.id} />
                  </Td>
                  <Td>{job.name}</Td>
                  <Td>{job.type}</Td>
                  <Td>{job.no_of_gpus}</Td>
                  <Td>{job.container_image}</Td>
                  <Td>{job.command}</Td>
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
