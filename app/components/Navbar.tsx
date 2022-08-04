import {
    Box,
    Flex,
    useColorMode,
    IconButton
} from '@chakra-ui/react'
import Navlink from './Navlink'
import Image from 'next/image'
import Switch from './Switch'

export default function Navigation(): JSX.Element {
    const { colorMode } = useColorMode();
    const imgUrl =
        colorMode === "light" ? "/image/icon.png" : "/image/icon-dark.png";
    return (
        <Box
            flexDirection="row"
            justifyContent="space-between"
            alignItems="center"
            height="100%"
            width="100%"
            as="nav"
            mt={10}
        >
            <Flex
                py={2}
                px={5}
                maxW="container.lg"
                align="center"
                mx="auto"
            >
                <Flex mr="auto">
                    <Navlink href="/">
                        <IconButton
                            aria-label="Schedulearn Icon"
                            icon={
                                <Image
                                    src={imgUrl}
                                    alt="Schedulearn Icon"
                                    height={32}
                                    width={32}
                                    priority
                                    quality={100}
                                    loading="eager"
                                />
                            }
                            color="white"
                            isRound
                            variant="ghost"
                            _hover={{
                                color: 'transparent'
                            }}
                        />
                    </Navlink>
                    <Navlink href="/jobs">Jobs</Navlink>
                </Flex>
                <Switch />
            </Flex>
        </Box>
    )
}