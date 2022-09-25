import {
  useDisclosure,
  chakra,
  Flex,
  HStack,
  Button,
  Box,
  IconButton,
  VStack,
  CloseButton,
  Text,
} from "@chakra-ui/react";
import React from "react";
import Link from "next/link";
import Image from "next/image";
import { HamburgerIcon } from "@chakra-ui/icons";

export default function MainNavbar() {
  const mobileNav = useDisclosure();
  return (
    <React.Fragment>
      <chakra.header
        w="full"
        px={{
          base: 2,
          sm: 4,
        }}
        py={4}
        shadow="md"
      >
        <Flex alignItems="center" justifyContent="space-between" mx="auto">
          <Link href="/">
            <Flex display="flex">
              <IconButton
                aria-label="Schedulearn Icon"
                icon={
                  <Image
                    src="/images/icon.png"
                    alt="Schedulearn Icon"
                    height={30}
                    width={30}
                  />
                }
                variant="ghost"
                _hover={{
                  textDecoration: "none",
                }}
              />
              <Text
                ml={1}
                my="auto"
                fontSize="xl"
                fontWeight="semibold"
                color="white"
              >
                Schedulearn
              </Text>
            </Flex>
          </Link>
          <HStack display="flex" alignItems="center" spacing={1}>
            <HStack
              spacing={1}
              mr={1}
              display={{
                base: "none",
                md: "inline-flex",
              }}
            >
              <Button variant="ghost"><Link href="/dashboard">Dashboard</Link></Button>
              <Button variant="ghost">Setting</Button>
              <Button colorScheme="red">Log out</Button>
            </HStack>
            <Box
              display={{
                base: "inline-flex",
                md: "none",
              }}
            >
              <IconButton
                display={{
                  base: "flex",
                  md: "none",
                }}
                icon={
                  <HamburgerIcon
                    w={5}
                    h={5}
                    display={mobileNav.isOpen ? "none" : "inherit"}
                  />
                }
                aria-label="Open menu"
                fontSize="20px"
                variant="ghost"
                onClick={mobileNav.onOpen}
              />
              <VStack
                pos="absolute"
                top={0}
                right={0}
                display={mobileNav.isOpen ? "flex" : "none"}
                flexDirection="column"
                p={2}
                pb={4}
                m={2}
                spacing={3}
                rounded="sm"
                shadow="sm"
                bg="black"
                width="100%"
              >
                <CloseButton
                  aria-label="Close menu"
                  onClick={mobileNav.onClose}
                />

                <Button w="full" variant="ghost">
                  <Link href="/dashboard">Dashboard</Link>
                </Button>
                <Button w="full" variant="ghost">
                  Setting
                </Button>
                <Button w="full" variant="ghost">
                  Log out
                </Button>
              </VStack>
            </Box>
          </HStack>
        </Flex>
      </chakra.header>
    </React.Fragment>
  );
}
