import {
  Box,
  Text,
  Menu,
  Link,
  HStack,
  VStack,
  IconButton,
  MenuItem,
  MenuList,
  MenuButton,
  MenuDivider,
  useBreakpointValue,
} from "@chakra-ui/react";
import NextLink from "next/link";
import { BiPencil } from "react-icons/bi";
import { HamburgerIcon } from "@chakra-ui/icons";
import { FiHome, FiUser } from "react-icons/fi";
import { MdOutlineWorkOutline } from 'react-icons/md';
import { useRouter } from "next/router";

function DropDownMenu() {
  const router = useRouter();

  const Signout = async () => {
    const res = await fetch(`http://localhost:8080/signout`, {
      method: "POST",
    });
    router.push("/");
  };

  return (
    <Menu isLazy>
      <MenuButton
        as={IconButton}
        icon={
          <HamburgerIcon
            color='gray.800'
            _dark={{
              color: 'whiteAlpha.900'
            }}
          />
        }
        isRound
        variant="ghost"
      />
      <MenuList
        zIndex={5}
        border="2px solid"
        borderColor="black.800"
        alignItems={["center", "flex-start"]}
        boxShadow="5px 5px 0px rgba(0, 0, 0, 0.1)"
        _dark={{
          borderColor: 'whiteAlpha.900',
          boxShadow: '5px 5px 0px rgba(255, 255, 255, 0.1)'
        }}
      >

        <MenuItem>
          <Text fontWeight="500">User 001</Text>
        </MenuItem>
        <MenuDivider />
        <NextLink href="/view_profile">
          <MenuItem fontWeight="500">
            <FiUser /><Text ml={2}>View Profile</Text>
          </MenuItem>
        </NextLink>
        <NextLink href="/jobs">
          <MenuItem fontWeight="500">
            < MdOutlineWorkOutline /><Text ml={2}>Jobs</Text>
          </MenuItem>
        </NextLink>
        <MenuItem fontWeight="500" onClick={Signout}>
          <FiHome /><Text ml={2}>Sign Out</Text>
        </MenuItem>
      </MenuList>
    </Menu>
  );
};

export default DropDownMenu;
