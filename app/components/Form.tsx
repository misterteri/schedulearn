
import {
    Box,
    Input,
    Button,
    Stack,
    FormControl,
    FormLabel,
    RadioGroup,
    Radio,
} from "@chakra-ui/react";
import { useState } from "react";
import { Controller, useForm } from "react-hook-form";
import AlertPop from "./AlertPop";

export default function Form(): JSX.Element {
    const {
        handleSubmit,
        register,
        control,
        formState: { errors, isSubmitting },
    } = useForm();

    const [submittedVal, setSubmittedVal] = useState();
    const isJobNameEmpty = errors.jobName ? true : false;
    const isJobTypeEmpty = errors.jobType ? true : false;
    const isJobImageEmpty = errors.jobImage ? true : false;
    const isJobCommandEmpty = errors.jobCommand ? true : false;
    const isRequiredGPUEmpty = errors.jobGPU ? true : false;

    const onSubmit = (data: any) => {
        setSubmittedVal(data);

        const json = {
            "jobName": data.jobName,
            "jobType": data.jobType,
            "jobImage": data.jobImage,
            "jobCommand": data.jobCommand,
            "jobGPU": parseInt(data.requiredGPU),
        }

        fetch("http://localhost:5000/post", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(
                json,
            ),
        })
            .then((res) => console.log("Success:", res))
            .catch((err) => console.error("Error:", err));
    };

    return (
        <Stack>
            <form onSubmit={handleSubmit(onSubmit)}>
                <FormControl isInvalid={isJobNameEmpty} my={10}>
                    <FormLabel> Name </FormLabel>
                    <Input
                        type="text"
                        placeholder="e.g. Sun Flower training"
                        {...register("jobName", {
                            required: { value: true, message: "Name is required" },
                            minLength: {
                                value: 3,
                                message: "Name must be at least 3 characters",
                            },
                        })}
                    />
                    {errors.jobName && <AlertPop title={errors.jobName.message} />}
                </FormControl>

                <FormControl isInvalid={isJobTypeEmpty} my={10}>
                    <FormLabel>Job Type</FormLabel>
                    <Controller
                        name="jobType"
                        control={control}
                        render={({ field }) => (
                            <RadioGroup {...field}>
                                <Stack direction="row">
                                    <Radio value="TensorFlow">TensorFlow</Radio>
                                    <Radio value="Pytorch">Pytorch</Radio>
                                    <Radio value="Keras">Keras</Radio>
                                    <Radio value="MXNet">MXNet</Radio>
                                </Stack>
                            </RadioGroup>
                        )}
                        rules={{
                            required: { value: true, message: "This is required." },
                        }}
                    />
                </FormControl>

                <FormControl isInvalid={isJobImageEmpty} my={10}>
                    <FormLabel>Docker Image Link</FormLabel>
                    <Input
                        type="url"
                        placeholder="e.g. https://hub.docker.com/r/sunflowerai/sunflower-tf-gpu"
                        {...register("jobImage", {
                            required: { value: true, message: "Docker Image is required." },
                        })}
                    />
                    {errors.jobImage && <AlertPop title={errors.jobImage.message} />}
                </FormControl>

                <FormControl isInvalid={isJobCommandEmpty} my={10}>
                    <FormLabel>Command</FormLabel>
                    <Input
                        type="text"
                        placeholder="e.g. python train.py"
                        {...register("jobCommand", {
                            required: { value: true, message: "Command is required." },
                        })}
                    />

                    {errors.jobCommand && (<AlertPop title={errors.jobCommand.message} />
                    )}
                </FormControl>

                <FormControl isInvalid={isRequiredGPUEmpty} my={10}>
                    <FormLabel>Required GPU(s)</FormLabel>
                    <Controller
                        name="requiredGPU"
                        control={control}
                        render={({ field }) => (
                            <RadioGroup {...field}>
                                <Stack direction="row">
                                    <Radio value="1">1</Radio>
                                    <Radio value="2">2</Radio>
                                    <Radio value="3">3</Radio>
                                    <Radio value="4">4</Radio>
                                </Stack>
                            </RadioGroup>
                        )}
                        rules={{
                            required: { value: true, message: "This is required." },
                        }}
                    />
                </FormControl>

                <Box my={10}>
                    <Button
                        colorScheme={"green"}
                        isLoading={false}
                        isDisabled={
                            isSubmitting ||
                            isJobNameEmpty ||
                            isJobTypeEmpty ||
                            isJobImageEmpty ||
                            isJobCommandEmpty ||
                            isRequiredGPUEmpty
                        }
                        variant="solid"
                        size="lg"
                        type="submit"
                    >
                        Submit
                    </Button>
                    {submittedVal && (
                        <div>
                            Submitted Data:
                            <br />
                            {JSON.stringify(submittedVal)}
                        </div>
                    )}
                </Box>
            </form>
        </Stack>
    );
}
