import { Alert, AlertIcon } from '@chakra-ui/react';

export default function AlertPop(props: any): JSX.Element {
    return (
        <Alert status='error'>
            <AlertIcon />
            There was an error processing your request
        </Alert>
    )
}