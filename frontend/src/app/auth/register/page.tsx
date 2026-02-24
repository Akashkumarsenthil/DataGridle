"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Card from "@/components/ui/Card";
import { api } from "@/lib/api";
import { useAuth } from "@/lib/auth-context";

export default function RegisterPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "user",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (form.password !== form.confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    setLoading(true);
    try {
      await api.post("/auth/register", {
        username: form.username,
        email: form.email,
        password: form.password,
        role: form.role,
      });
      await login(form.email, form.password);
      router.push("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  const update = (field: string) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((prev) => ({ ...prev, [field]: e.target.value }));

  return (
    <div className="flex min-h-[calc(100vh-4rem)] items-center justify-center px-4 py-12">
      <Card className="w-full max-w-md">
        <div className="mb-8 text-center">
          <h1 className="text-2xl font-bold text-white">Create Account</h1>
          <p className="mt-2 text-sm text-gray-400">Start mastering data interviews today</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          {error && (
            <div className="rounded-lg border border-red-500/20 bg-red-500/10 p-3 text-sm text-red-400">
              {error}
            </div>
          )}

          <Input
            label="Username"
            placeholder="datawizard"
            value={form.username}
            onChange={update("username")}
            required
          />

          <Input
            label="Email"
            type="email"
            placeholder="you@example.com"
            value={form.email}
            onChange={update("email")}
            required
          />

          <Input
            label="Password"
            type="password"
            placeholder="Min 8 characters"
            value={form.password}
            onChange={update("password")}
            required
            minLength={8}
          />

          <Input
            label="Confirm Password"
            type="password"
            placeholder="Repeat your password"
            value={form.confirmPassword}
            onChange={update("confirmPassword")}
            required
          />

          <div className="space-y-2">
            <p className="text-sm font-medium text-gray-300">Account type</p>
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => setForm((prev) => ({ ...prev, role: "user" }))}
                className={`flex-1 rounded-lg border px-3 py-2 text-sm ${
                  form.role === "user"
                    ? "border-green-500 bg-green-500/10 text-green-300"
                    : "border-gray-700 bg-gray-900 text-gray-300"
                }`}
              >
                <div className="font-medium">Learner</div>
                <div className="mt-0.5 text-xs text-gray-400">
                  Solve questions, track progress.
                </div>
              </button>
              <button
                type="button"
                onClick={() => setForm((prev) => ({ ...prev, role: "creator" }))}
                className={`flex-1 rounded-lg border px-3 py-2 text-sm ${
                  form.role === "creator"
                    ? "border-blue-400 bg-blue-500/10 text-blue-200"
                    : "border-gray-700 bg-gray-900 text-gray-300"
                }`}
              >
                <div className="font-medium">Creator</div>
                <div className="mt-0.5 text-xs text-gray-400">
                  Request to submit questions (admin approval required).
                </div>
              </button>
            </div>
            <p className="text-xs text-gray-500">
              Learner accounts get full access immediately. Creator accounts can log in
              but need admin approval before publishing content.
            </p>
          </div>

          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? "Creating account..." : "Sign Up"}
          </Button>
        </form>

        <div className="mt-6 text-center text-sm text-gray-400">
          Already have an account?{" "}
          <Link href="/auth/login" className="text-green-400 hover:text-green-300">
            Log in
          </Link>
        </div>
      </Card>
    </div>
  );
}
