import {
    Box,
    Flex,
} from '@chakra-ui/react'
import Navlink from './Navlink'
import { RepeatIcon } from '@chakra-ui/icons'
import Switch from './Switch'

export default function Navigation(): JSX.Element {
    return (
        <Box
            flexDirection="row"
            justifyContent="space-between"
            alignItems="center"
            height="100%"
            width="100%"
            as="nav"
        >
            <Flex
                py={2}
                px={5}
                maxW="container.md"
                align="center"
                mx="auto"
            >
                <Flex mr="auto">
                    <Navlink href="/"><RepeatIcon w={5} h={5} /></Navlink>
                    <Navlink href="/jobs">Jobs</Navlink>
                </Flex>
                <Switch />
            </Flex>
        </Box>
    )
}