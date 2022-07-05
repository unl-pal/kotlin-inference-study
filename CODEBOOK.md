# Codebook for Kotlin Inference Study

## Substitutions Available

 - `{@escape@}`
: Logic to escape filenames for output to avoid errors with special characters in CSV-ification process.

 - `{@project-filter@}`
: Filter projects to remove those which are not relevant or should be excluded.

 - `{@time-out@}`
: Output index descriptor for time-based queries.

 - `{@time-part@}`
: Output of current revision and current time for time-based queries.

 - `{@time-or-snapshot@}`
: Either snapshot or at each revision, output base files.

## Output Files

### `dupes.csv`

1. `hash`
: AST Hash of the file at HEAD, `long`.

2. `project`
: Project ID, `string`/`integer`.

3. `url`
: Filename relative to repository root, `string`.

### `basic-usage.csv`

1. `project`
: Project ID, `string`/`integer`

2. `file`
: Filename relative to repository root, `string`.

3. `location`
: Overall location of declaration, `string`, one of
   - `return_val`
   - `lambda_arg`
   - `body`
   - `module`

4. `isval`
: Whether or not location is declared as `val`, `boolean`, `true` if `val`, `false` if `var`.

5. `isinferred`
: Whether or not the location uses type inference, `boolean`.

6. `count`
: Number of declarations fitting items 1--5, `long`.

### `over-time.txt`

1. `project`
: Project ID, `string`/`integer`

2. `revision`
: SHA of revision collected, `string`.

3. `time`
: Time of revision, `long` representing microseconds since Unix epoch.

4. `file`
: Filename relative to repository root, `string`.

5. `location`
: Overall location of declaration, `string`, one of
   - `return_val`
   - `lambda_arg`
   - `body`
   - `module`

6. `isval`
: Whether or not location is declared as `val`, `boolean`, `true` if `val`, `false` if `var`.

7. `isinferred`
: Whether or not the location uses type inference, `boolean`.

8. `count`
: Number of declarations fitting items 1--5, `long`.

### `rhs.csv`

### `survival.csv`

### `count-unfiltered.csv`, `count-filtered.csv`

1. `type`
: The type of `count`, `string`.

2. `filtered`
: Whether or not count is from filtered data, `boolean`.

3. `count`
: Count of items described by `type`, `long`.
