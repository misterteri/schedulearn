import React from "react";
import {
    AlertDialog,
    AlertDialogBody,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogContent,
    AlertDialogOverlay,
    IconButton,
    AlertDialogCloseButton,
    useDisclosure,
    useToast,
} from "@chakra-ui/react";
import { Button } from "@chakra-ui/react";
import { DeleteIcon } from "@chakra-ui/icons";

function DeleteButton({ id }: { id: number }) {
    const toast = useToast()

    const handleDeleteJob = async () => {
        const res = await fetch(`http://localhost:5000/jobs/${id}`, {
            method: "DELETE",
        });
        window.location.reload();
        const data = await res.json();
        console.log(data);
        toast({
            title: "Job deleted",
            description: "The job has been deleted",
            status: "success",
            duration: 9000,
        })
    };

    const { isOpen, onOpen, onClose } = useDisclosure();
    const cancelRef = React.useRef();

    return (
        <>
            <IconButton
                icon={<DeleteIcon />}
                mr="2"
                onClick={() => onOpen()}
                isRound
                variant="ghost"
                aria-label={""}
            />
            <AlertDialog
                motionPreset="slideInBottom"
                // @ts-ignore
                leastDestructiveRef={cancelRef}
                onClose={onClose}
                isOpen={isOpen}
                isCentered
            >
                <AlertDialogOverlay />

                <AlertDialogContent>
                    <AlertDialogHeader>Delete this model ?</AlertDialogHeader>
                    <AlertDialogCloseButton />
                    <AlertDialogBody>
                        Are you sure you want to delete the job?
                    </AlertDialogBody>
                    <AlertDialogFooter>
                        <Button onClick={onClose}>No</Button>
                        <Button colorScheme="red" ml={3} onClick={handleDeleteJob}>
                            Yes
                        </Button>
                    </AlertDialogFooter>
                </AlertDialogContent>
            </AlertDialog>
        </>
    );
}

export default DeleteButton;
