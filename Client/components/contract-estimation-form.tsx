"use client"

import { useState } from "react"
import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useToast } from "@/components/ui/use-toast"
import { submitContractData, type ContractFormData } from "@/services/api"

const formSchema = z.object({
  contractSize: z.string().min(1, "Contract size is required"),
  distance: z.string().min(1, "Distance is required"),
  projectSize: z.string().min(1, "Project size is required"),
  projectType: z.string().min(1, "Project type is required"),
  otherContractors: z.string().min(1, "Number of other contractors is required"),
})

export default function ContractEstimationForm() {
  const [isSubmitting, setIsSubmitting] = useState(false)
  const { toast } = useToast()

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      contractSize: "",
      distance: "",
      projectSize: "",
      projectType: "",
      otherContractors: "",
    },
  })

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsSubmitting(true)
    try {
      const result = await submitContractData(values as ContractFormData)
      toast({
        title: "Form submitted",
        description: "Your contract data has been successfully submitted.",
      })
      form.reset()
    } catch (error) {
      toast({
        title: "Submission failed",
        description: "There was an error submitting your data. Please try again.",
        variant: "destructive",
      })
      console.error(error)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="p-6 bg-card text-card-foreground shadow-lg rounded-lg">
      <h2 className="text-2xl font-semibold mb-4">Contract Estimation Form</h2>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
          <FormField
            control={form.control}
            name="contractSize"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Estimated Contract Size ($)</FormLabel>
                <FormControl>
                  <Input type="number" placeholder="Enter estimated contract size" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="distance"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Distance from Project (miles)</FormLabel>
                <FormControl>
                  <Input type="number" placeholder="Enter distance from project" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="projectSize"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Project Size (sq ft)</FormLabel>
                <FormControl>
                  <Input type="number" placeholder="Enter total finished square feet" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="projectType"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Project Type</FormLabel>
                <Select onValueChange={field.onChange} defaultValue={field.value}>
                  <FormControl>
                    <SelectTrigger>
                      <SelectValue placeholder="Select project type" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem value="educational">Educational</SelectItem>
                    <SelectItem value="residential">Residential</SelectItem>
                    <SelectItem value="government">Government</SelectItem>
                    <SelectItem value="commercial">Commercial</SelectItem>
                    <SelectItem value="industrial">Industrial</SelectItem>
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="otherContractors"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Number of Other General Contractors Bidding</FormLabel>
                <FormControl>
                  <Input type="number" placeholder="Enter number of other contractors" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? "Submitting..." : "Submit"}
          </Button>
        </form>
      </Form>
    </div>
  )
}

