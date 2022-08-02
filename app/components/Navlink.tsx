import { Link } from '@chakra-ui/react'
import NextLink from 'next/link'
import { useRouter } from 'next/router'

export default function Navlink({ href, children }: { href: string, children: React.ReactNode }): JSX.Element {
    const router = useRouter()
    var isActive = router.pathname === href

    if (href.includes("blog")) {
        isActive = router.pathname.includes("/blog")
    }

    if (href.includes("portfolio")) {
        isActive = router.pathname.includes("/portfolio")
    }

    return (
        <NextLink href={href}>
            <Link
                mr={5}
                variant="ghost"
                fontWeight="semibold"
                color={isActive ? 'black' : 'gray.400'}
                _hover={{ color: 'black' }}
                _active={{ color: 'black' }}
                _dark={{
                    color: isActive ? 'white' : 'gray.400',
                    '&:hover': {
                        color: 'white'
                    },
                    '&:active': {
                        color: 'white'
                    }
                }}
            >{children}</Link>
        </NextLink>
    )
}