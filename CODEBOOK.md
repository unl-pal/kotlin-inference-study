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

- `{@locations-enum@}`
: An enum describing possible locations.

 - `{@get-method-signature@}`
: Provides function `getMethodSignature(string, string, Method): string`, which takes a package name, a class name, and a method returning a JVM Bytecode formatted method signature.

## Output Files

### `dupes.csv`

1. `hash`
: AST Hash of the file at HEAD, `long`.

2. `project`
: Project ID, `string`/`integer`.

3. `url`
: Filename relative to repository root, `string`.

### `basic-usage.csv`

1. `project` (`string`/`integer`)
: Project ID.

2. `file` (`string`)
: Filename relative to repository root.

3. `location` (`string`, *restricted*)
: Overall location of declaration, `string`, one of
   - `return_val`
   - `lambda_arg`
   - `body`
   - `module`

4. `isval` (`boolean`)
: Whether or not location is declared as `val` (`true` if `val`, `false` if `var`).

5. `isinferred` (`boolean`)
: Whether or not the location uses type inference.

6. `count` (`long`)
: Number of declarations fitting items 1--5.

### `over-time.txt`

1. `project` (`string`/`integer`)
: Project ID.

2. `revision` (`string`)
: SHA of revision collected.

3. `time` (`long`)
: Time of revision as microseconds since Unix epoch.

4. `file` (`string`)
: Filename relative to repository root.

5. `location` (`string`, *restricted*)
: Overall location of declaration, *see `basic-usage.csv`/`location`*.

6. `isval` (`boolean`)
: Whether or not location is declared as `val` (`true` if `val`, `false` if `var`).

7. `isinferred` (`boolean`)
: Whether or not the location uses type inference.

8. `count` (`long`)
: Number of declarations fitting items 1--7.

### `rhs.csv`

### `survival.csv`

1. `project` (`string`/`integer`)
: Project ID.

2. `file` (`string`)
: Filename relative to repository root, `string`.

3. `item` (`string`)
: Fully-qualified name of observation.

4. `location` (`string`, *restricted*)
: Overall location of declaration, `string`, see `basic-usage.csv`/`location`.

5. `startinferred` (`boolean`)
: Whether or not the observation starts inferred.

6. `changekind` (`string`, *restricted*)
: The sort of change recorded.  Options are `file_deletion` (file with this item is removed without changing state), `item_disappearance` (item dissappears without changing state), `state_switch` (item changes state from inferred to not inferred or vice versa).

7. `observed` (`boolean`)
: Observation right-censoring.  `true` if a change in inference status (i.e., annotation presence) is observed, `false` if no change is observed before "death" (deletion or end of history) of `item`.

8. `timetochange` (`long`)
: How long (in microseconds) before a change or end of history (see `observed`).

### `count-unfiltered.csv`, `count-filtered.csv`

1. `type` (`string`, *restricted*)
: The type of `count`.  Possible values are
    - `projects`
    - `total_files_head`
    - `analyzed_files_head`
    - `total_files_hist`
    - `analyzed_files_hist`

2. `filtered` (`boolean`)
: Whether or not count is from filtered data.

3. `count` (`long`)
: Count of items described by `type`.
