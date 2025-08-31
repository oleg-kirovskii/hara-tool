from openai import OpenAI

class HazopAIClient:
    def __init__(self):
        self.client = OpenAI()
        self.system_prompt = """You are a HAZOP analysis expert. For each function and keyword combination, 
        provide a brief, specific description of a potential malfunction. 
        The response shall be one sentence.

        Meaning of keywords:
        - No: Complete negation of the function.
        - More: Function occurs to a greater extent than intended.
        - Less: Function occurs to a lesser extent than intended.
        - As well as: An additional function occurs alongside the intended function.
        - Part of: Only a portion of the function occurs.
        - Reverse: The opposite of the intended function occurs.
        - Other than: A different function occurs instead of the intended one.
        - Early: The function occurs before it is supposed to.
        - Late: The function occurs after it is supposed to.
        - Before: The function occurs prior to a specified event or condition.
        - After: The function occurs following a specified event or condition.
        - Not: The function fails to occur when it should.    

        Example 1:
        - Function: The system shall measure temperature.
        - Keyword: Not
        - Malfunction: The system does not measure temperature.
        """

    def get_malfunction(self, combination):
        """Get malfunction description from OpenAI for a function-keyword pair."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Describe a malfunction when {combination['function']} experiences condition: {combination['keyword']}"}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=150
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error getting response from OpenAI: {e}")
            return None