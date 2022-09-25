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
import { useRouter } from "next/router";

function DeleteButton({ id }: { id: number }) {
  const toast = useToast();
  const router = useRouter();

  const handleDeleteJob = async () => {
    const res = await fetch(`http://localhost:8080/jobs/${id}`, {
      method: "DELETE",
    });

    toast({
      title: "Success",
      description: "Job has been deleted",
      status: "success",
      duration: 5000,
      isClosable: true,
    });

    router.push("/jobs");
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
            <Button colorScheme="green" ml={3} onClick={handleDeleteJob}>
              Yes
            </Button>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
}

export default DeleteButton;
