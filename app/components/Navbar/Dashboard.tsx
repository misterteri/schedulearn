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
import Dropdown from "../Logout/Dropdown";
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
            <Dropdown />
          </HStack>
        </Flex>
      </chakra.header>
    </React.Fragment>
  );
}
